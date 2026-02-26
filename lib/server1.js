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
    res.setHeader('X-Server-ID', 'server1-javascript');
    next();
});

app.get('/getDrinks/all', (req, res) => {
    const data = loadData();
    res.json(data.drinks);
});

app.get('/getDrink/byId/:id', (req, res) => {
    const data = loadData();
    const drink = data.drinks.find(d => d.id === parseInt(req.params.id));
    if (!drink) {
        return res.status(404).json({ error: 'Nápoj nenalezen' });
    }
    res.json(drink);
});

app.post('/createDrink', (req, res) => {
    const data = loadData();
    const newDrink = req.body;

    if (!newDrink.name || !newDrink.price) {
        return res.status(400).json({ error: 'Chybí povinné údaje' });
    }

    let newId = 1;
    if (data.drinks.length > 0) {
        newId = Math.max(...data.drinks.map(d => d.id)) + 1;
    }

    newDrink.id = newId;
    data.drinks.push(newDrink);
    saveData(data);

    res.status(201).json(newDrink);
});

app.put('/updateDrink/:id', (req, res) => {
    const data = loadData();
    const id = parseInt(req.params.id);
    const updateData = req.body;

    const index = data.drinks.findIndex(d => d.id === id);
    if (index === -1) {
        return res.status(404).json({ error: 'Nápoj nenalezen' });
    }

    updateData.id = id;
    data.drinks[index] = updateData;
    saveData(data);

    res.json(updateData);
});


app.listen(8001, () => {
    console.log('Server 1 běží na portu 8001');
});
