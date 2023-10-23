require ('dotenv').config();
const PORT = process.env.PORT;
const cors = require('cors');
const express = require('express');

const app = express()


app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`)
});