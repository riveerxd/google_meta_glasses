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

app.get('/getAnimals/all', (req, res) => {
    const data = loadData();
    res.json(data.animals);
});

app.get('/getAnimal/byId/:id', (req, res) => {
    const data = loadData();
    const animal = data.animals.find(a => a.id === parseInt(req.params.id));
    if (!animal) {
        return res.status(404).json({ error: 'Zvíře nenalezeno' });
    }
    res.json(animal);
});

app.post('/createAnimal', (req, res) => {
    const data = loadData();
    const newAnimal = req.body;

    if (!newAnimal.name || !newAnimal.species) {
        return res.status(400).json({ error: 'Chybí povinné údaje' });
    }

    let newId = 1;
    if (data.animals.length > 0) {
        newId = Math.max(...data.animals.map(a => a.id)) + 1;
    }

    newAnimal.id = newId;
    data.animals.push(newAnimal);
    saveData(data);

    res.status(201).json(newAnimal);
});

app.put('/updateAnimal/:id', (req, res) => {
    const data = loadData();
    const id = parseInt(req.params.id);
    const updateData = req.body;

    const index = data.animals.findIndex(a => a.id === id);
    if (index === -1) {
        return res.status(404).json({ error: 'Zvíře nenalezeno' });
    }

    updateData.id = id;
    data.animals[index] = updateData;
    saveData(data);

    res.json(updateData);
});


app.listen(8001, () => {
    console.log('Server 1 běží na portu 8001');
});
