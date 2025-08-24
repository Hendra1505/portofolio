import express from "express";
import helmet from "helmet";
import morgan from "morgan";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();

const PORT = process.env.PORT;
// const cors = require('cors');
// const express = require('express');

const app = express();

app.use(express.json());
app.use(cors());
app.use(helmet()); // helmet adalah security middleware yang membantu kita untuk melindungi app dari berbagai banyak-nya HTTP headers  
app.use(morgan("dev")); // Log the request

app.get("/test", (req, res) => {
    console.log(res.getHeaders());
    res.send("Hello from the test route");
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`)
});