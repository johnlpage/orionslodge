exports = async function(angle){
  
    
    const collection = context.services.get("mongodb-atlas").db("motion").collection("steertruck");
    const driver = context.user.id
    const truck = "henglong"
   
    
    const query = { _id : truck }
    const update={ $set : {  driver: driver }} 
    return await collection.updateOne(query,update,{upsert:true})
  
};