var mongoose = require("../db/mongoose");
var LOG = require('../logger/logger').logger
var Schema = mongoose.Schema;

var CorpusSchema = new Schema({
    _id: {type: String},
}, { strict: false });
var Corpus = mongoose.model('Singlecorpus', CorpusSchema, 'sentencelog');

Corpus.fetchAll = function(id, cb){
    Corpus.find({
    }, function (err, corpus) {
        if (err) {
            LOG.error("Unable to find corpus due to [%s]", JSON.stringify(err));
            return cb(err, null);
        }
        // LOG.info("[%s] Corpus found",corpus);
        corpus.map((c)=>{
            var value = 0
            if(c._doc.target_edited_words && Array.isArray(c._doc.target_edited_words)){
                c._doc.target_edited_words.map((word)=>{
                    if(c._doc.target.indexOf(word)<0){
                        console.log(word)
                        console.log(c._doc.target)
                        value++;
                    }
                })
            }
            console.log(value)
        })
        return cb(null, corpus);
    })
}

if(process.argv.length>2){
    // console.log(process.argv[2]);
    Corpus.fetchAll(process.argv[2],function(err, corpus){
        // console.log(corpus.length)
    })
}


module.exports = Corpus;
