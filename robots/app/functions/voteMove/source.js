exports = async function(vote){
    largomoves = ["tiltup","tiltdown","panleft","panright"];
    
    const collection = context.services.get("mongodb-atlas").db("motion").collection("votes");
    const voter = context.user.id
    var hostname = "umberto";
    if(largomoves.includes(vote)) {
      hostname = "largo";
    }
    
    const query = { _id : hostname, voters : { $ne : voter} }
    const update={ $push : { voters: voter }, $inc : { votes : 1 }} 
    update["$inc"][vote]=1
  try { 
    await collection.updateOne(query,update,{upsert:true})
  } catch(e) {
    console.log(e)
  }
    return;
};