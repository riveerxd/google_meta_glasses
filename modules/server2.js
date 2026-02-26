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

app.get('/getProtocols/all', (req, res) => {
    const data = loadData();
    let protocols = data.protocols;

    const statusFilter = req.query.status;
    if (statusFilter) {
        protocols = protocols.filter(p => p.status === statusFilter);
    }

    res.json(protocols);
});

app.get('/getProtocol/byId/:id', (req, res) => {
    const data = loadData();
    const protocol = data.protocols.find(p => p.id === parseInt(req.params.id));
    if (!protocol) {
        return res.status(404).json({ error: 'Protokol nenalezen' });
    }
    res.json(protocol);
});

app.post('/createProtocol', (req, res) => {
    const data = loadData();
    const newProtocol = req.body;

    if (!newProtocol.location || !newProtocol.date) {
        return res.status(400).json({ error: 'Chybí povinné údaje' });
    }

    let newId = 1;
    if (data.protocols.length > 0) {
        newId = Math.max(...data.protocols.map(p => p.id)) + 1;
    }

    newProtocol.id = newId;
    data.protocols.push(newProtocol);
    saveData(data);

    res.status(201).json(newProtocol);
});

app.delete('/deleteProtocol/:id', (req, res) => {
    const data = loadData();
    const id = parseInt(req.params.id);

    const index = data.protocols.findIndex(p => p.id === id);
    if (index === -1) {
        return res.status(404).json({ error: 'Protokol nenalezen' });
    }

    const deleted = data.protocols.splice(index, 1)[0];
    saveData(data);

    res.json(deleted);
});


app.listen(8002, () => {
    console.log('Server 2 běží na portu 8002');
});
