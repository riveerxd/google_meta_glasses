const express = require('express');
const fs = require('fs');

const app = express();
app.use(express.json());

function loadData() {
    return JSON.parse(fs.readFileSync('db.json', 'utf-8'));
}

function saveData(data) {
    fs.writeFileSync('db.json', JSON.stringify(data, null, 2));
}

app.use((req, res, next) => {
    res.setHeader('X-Server-ID', 'server2-javascript');
    next();
});

app.get('/getRecords/all', (req, res) => {
    const data = loadData();
    res.json(data.records);
});

app.get('/getRecord/byId/:id', (req, res) => {
    const data = loadData();
    const record = data.records.find(r => r.id === parseInt(req.params.id));
    if (!record) {
        return res.status(404).json({ error: 'Záznam nenalezen' });
    }
    res.json(record);
});

app.post('/createRecord', (req, res) => {
    const data = loadData();
    const newRecord = req.body;

    if (!newRecord.client || !newRecord.date) {
        return res.status(400).json({ error: 'Chybí povinné údaje' });
    }

    let newId = 1;
    if (data.records.length > 0) {
        newId = Math.max(...data.records.map(r => r.id)) + 1;
    }

    newRecord.id = newId;
    data.records.push(newRecord);
    saveData(data);

    res.status(201).json(newRecord);
});

app.put('/updateRecord/:id', (req, res) => {
    const data = loadData();
    const id = parseInt(req.params.id);
    const updateData = req.body;

    const index = data.records.findIndex(r => r.id === id);
    if (index === -1) {
        return res.status(404).json({ error: 'Záznam nenalezen' });
    }

    updateData.id = id;
    data.records[index] = updateData;
    saveData(data);

    res.json(updateData);
});


app.listen(8002, () => {
    console.log('Server 2 běží na portu 8002');
});
