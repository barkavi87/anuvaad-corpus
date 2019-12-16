var Response = require('../models/response')
var APIStatus = require('../errors/apistatus')
var ParagraphWorkspace = require('../models/paragraph_workspace');
var StatusCode = require('../errors/statuscodes').StatusCode
var LOG = require('../logger/logger').logger
var KafkaProducer = require('../kafka/producer');
var fs = require('fs');
var UUIDV4 = require('uuid/v4')
var COMPONENT = "workspace";
const BASE_PATH_PIPELINE_1 = 'corpusfiles/processing/pipeline_stage_1/'
const STATUS_PROCESSING = 'PROCESSING'
const STATUS_PROCESSED = 'PROCESSED'
const STEP_UPLOAD_PRAGRAPH = 'UPLOAD_PRAGRAPH'


exports.fetchParagraphWorkspace = function (req, res) {
    let status = req.query.status
    var pagesize = req.query.pagesize
    var pageno = req.query.pageno
    let condition = {}
    if (status === STATUS_PROCESSING) {
        condition = { status: STATUS_PROCESSING, stage: 1 }
    } else {
        condition = { status: STATUS_PROCESSED, stage: 1 }
    }
    ParagraphWorkspace.countDocuments(condition, function (err, count) {
        if (err) {
            LOG.error(err)
            let apistatus = new APIStatus(StatusCode.ERR_GLOBAL_SYSTEM, COMPONENT).getRspStatus()
            return res.status(apistatus.http.status).json(apistatus);
        }
        ParagraphWorkspace.findByCondition(condition, pagesize, pageno, function (err, models) {
            if (err) {
                LOG.error(err)
                let apistatus = new APIStatus(StatusCode.ERR_GLOBAL_SYSTEM, COMPONENT).getRspStatus()
                return res.status(apistatus.http.status).json(apistatus);
            }
            let response = new Response(StatusCode.SUCCESS, models, count).getRsp()
            return res.status(response.http.status).json(response);
        })
    })
}

exports.saveParagraphWorkspace = function (req, res) {
    if (!req || !req.body || !req.body.paragraph_workspaces || !Array.isArray(req.body.paragraph_workspaces) || req.body.paragraph_workspaces.length <= 0) {
        let apistatus = new APIStatus(StatusCode.ERR_GLOBAL_MISSING_PARAMETERS, COMPONENT).getRspStatus()
        return res.status(apistatus.http.status).json(apistatus);
    }
    req.body.paragraph_workspaces.map((workspace) => {
        workspace.session_id = UUIDV4()
        fs.mkdir(BASE_PATH_PIPELINE_1 + workspace.session_id, function (e) {
            fs.mkdir(BASE_PATH_PIPELINE_1 + workspace.session_id, function (e) {
                fs.copyFile('nginx/' + workspace.config_file_location, BASE_PATH_PIPELINE_1 + workspace.session_id + '/' + workspace.config_file_location, function (err) {
                    if (err) {
                        LOG.error(err)
                        let apistatus = new APIStatus(StatusCode.ERR_GLOBAL_SYSTEM, COMPONENT).getRspStatus()
                        return res.status(apistatus.http.status).json(apistatus);
                    }
                    else {
                        fs.copyFile('nginx/' + workspace.csv_file_location, BASE_PATH_PIPELINE_1 + workspace.session_id + '/' + workspace.csv_file_location, function (err) {
                            if (err) {
                                LOG.error(err)
                                let apistatus = new APIStatus(StatusCode.ERR_GLOBAL_SYSTEM, COMPONENT).getRspStatus()
                                return res.status(apistatus.http.status).json(apistatus);
                            }
                            req.body.paragraph_workspaces.map((workspace) => {
                                workspace.status = STATUS_PROCESSING
                                workspace.stage = 1
                                workspace.step = STEP_UPLOAD_PRAGRAPH
                            })
                            ParagraphWorkspace.save(req.body.paragraph_workspaces, function (err, models) {
                                if (err) {
                                    let apistatus = new APIStatus(StatusCode.ERR_GLOBAL_SYSTEM, COMPONENT).getRspStatus()
                                    return res.status(apistatus.http.status).json(apistatus);
                                }
                                models.ops.map((data) => {
                                    KafkaProducer.getInstance().getProducer((err, producer) => {
                                        if (err) {
                                            LOG.error("Unable to connect to KafkaProducer");
                                        } else {
                                            LOG.info("KafkaProducer connected")
                                            let payloads = [
                                                {
                                                    topic: 'tokenext', messages: JSON.stringify({ data: data }), partition: 0
                                                }
                                            ]
                                            producer.send(payloads, function (err, data) {
                                                LOG.info('Produced')
                                            });
                                        }
                                    })
                                })

                                let response = new Response(StatusCode.SUCCESS, COMPONENT).getRsp()
                                return res.status(response.http.status).json(response);
                            })
                        });
                    }
                });
            })
        });
    })


}