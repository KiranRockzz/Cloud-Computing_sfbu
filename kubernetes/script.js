const MongoClient = require('mongodb').MongoClient;
const url = "mongodb://35.193.87.8/studentdb";  // Update to your actual MongoDB URL and database

(async function() {
  let client;
  try {
    client = await MongoClient.connect(url);
    const db = client.db('studentdb'); // Use the correct database name
    const docs = [
      { student_id: 11111, student_name: "Bruce Lee", grade: 84 },
      { student_id: 22222, student_name: "Jackie Chen", grade: 93 },
      { student_id: 33333, student_name: "Jet Li", grade: 88 }
    ];

    const insertResult = await db.collection('students').insertMany(docs);
    console.log('Documents inserted:', insertResult.insertedCount);

    const findResult = await db.collection('students').findOne({ student_id: 11111 });
    console.log('Found document:', findResult);
  } catch (err) {
    console.error('An error occurred:', err);
  } finally {
    if (client) {
      client.close();
    }
  }
})();