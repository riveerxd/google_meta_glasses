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

app.get('/getTickets/all', (req, res) => {
    const data = loadData();
    res.json(data.tickets);
});

app.get('/getTicket/byId/:id', (req, res) => {
    const data = loadData();
    const ticket = data.tickets.find(t => t.id === parseInt(req.params.id));
    if (!ticket) {
        return res.status(404).json({ error: 'Vstupenka nenalezena' });
    }
    res.json(ticket);
});

app.post('/createTicket', (req, res) => {
    const data = loadData();
    const newTicket = req.body;

    if (!newTicket.name || !newTicket.table) {
        return res.status(400).json({ error: 'Chybí povinné údaje' });
    }

    let newId = 1;
    if (data.tickets.length > 0) {
        newId = Math.max(...data.tickets.map(t => t.id)) + 1;
    }

    newTicket.id = newId;
    data.tickets.push(newTicket);
    saveData(data);

    res.status(201).json(newTicket);
});

app.put('/updateTicket/:id', (req, res) => {
    const data = loadData();
    const id = parseInt(req.params.id);
    const updateData = req.body;

    const index = data.tickets.findIndex(t => t.id === id);
    if (index === -1) {
        return res.status(404).json({ error: 'Vstupenka nenalezena' });
    }

    updateData.id = id;
    data.tickets[index] = updateData;
    saveData(data);

    res.json(updateData);
});


app.listen(8002, () => {
    console.log('Server 2 běží na portu 8002');
});
