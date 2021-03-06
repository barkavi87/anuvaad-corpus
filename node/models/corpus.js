var mongoose = require("../db/mongoose");
var LOG = require('../logger/logger').logger
var Schema = mongoose.Schema;

var CorpusSchema = new Schema({
    _id: {type: String},
}, { strict: false });
var Corpus = mongoose.model('Corpus', CorpusSchema, 'corpus');

Corpus.findByCondition = function(condition, cb){
    Corpus.find(condition, function (err, corpus) {
        if (err) {
            LOG.error("Unable to find corpus due to [%s]", JSON.stringify(err));
            return cb(err, null);
        }
        return cb(null, corpus);
    })
} 

Corpus.fetchAll = function(cb){
    Corpus.find({
    }, function (err, corpus) {
        if (err) {
            LOG.error("Unable to find corpus due to [%s]", JSON.stringify(err));
            return cb(err, null);
        }
        LOG.debug("[%s] Corpus found",corpus);
        return cb(null, corpus);
    })
}

Corpus.updateCorpus = function (corpus, cb) {
    Corpus.collection.findOneAndUpdate({ _id: mongoose.Types.ObjectId(corpus._id)}, { $set: { data_processed: corpus.data_processed, status: corpus.status} }, { upsert: false }, function (err, doc) {
        if (err) {
            LOG.error(err)
            cb(err, null)
        }
        cb(null, doc)
    });
}

Corpus.saveCorpus = function(corpus, cb){
    Corpus.collection.insert(corpus,function(err,docs){
        if (err) {
            // TODO: handle error
            return cb(err, null);
        } else {
            LOG.debug('%s corpus was successfully stored.', JSON.stringify(docs));
            return cb(null, docs);
        }
    })
}


module.exports = Corpus;
