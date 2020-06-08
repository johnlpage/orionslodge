exports = function(changeEvent) {

    
    const collection = context.services.get("mongodb-atlas").db("vision").collection("frames");
    const driver = context.user.id
    const truck = "umberto"
    
    collection.updateOne({_id:truck},{$set:{lastfeed:new Date()},$inc:{energy:200}},{upsert:true})
    console.log(JSON.stringify(changeEvent))
    
};
