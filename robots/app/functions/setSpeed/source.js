exports = async function(speed){
  
    
    const collection = context.services.get("mongodb-atlas").db("motion").collection("steertruck");
    const driver = context.user.id
    const truck = "henglong"
   
    
    const query = { _id : truck, driver:driver }
    const update={ $set : { speed: speed,  when : new Date() }} 
    try {
    return await collection.updateOne(query,update,{upsert:true})
    } catch(e) {
      console.log("not controller")
      return "not controller"
    }
  
};