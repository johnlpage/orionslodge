exports = async function(angle){
  
    
    const collection = context.services.get("mongodb-atlas").db("motion").collection("steertruck");
    const driver = context.user.id
    const truck = "henglong"
   
    
    const query = { _id : truck , driver: driver}
    
    const update={ $set : { angle: angle, when : new Date() }} 
    try {
     await collection.updateOne(query,update,{upsert:true})
     return "ok";
    } 
    catch(err) {
      return "not controller"
    }

};