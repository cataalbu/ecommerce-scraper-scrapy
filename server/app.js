import express from 'express';
import {config} from "dotenv";
import bodyParser from 'body-parser';
import { spawn } from 'child_process';
import path from 'path';

config({path: `.env.server`})

const app = express();
const port = process.env.PORT || 3000;

console.log(process.cwd())

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const venvPythonPath = path.join('venv', 'bin', 'python')


app.route('/csr').get((req, res) => {
      try {

          const child_process = spawn(venvPythonPath, [path.join('ecommerce_scraper', 'tasks', 'csrscrapetask.py')], {
              cwd: process.cwd(),
              env: {
                  PYTHONPATH: path.join('ecommerce_scraper')
              }
          })

          child_process.stdout.on('data', (data) => {
              console.log(`stdout: ${data}`);
            });

            child_process.stderr.on('data', (data) => {
              console.error(`stderr: ${data}`);
            });

            child_process.on('close', (code) => {
              console.log(`child process exited with code ${code}`);
            });

            return res.json({ message: 'Scrape CSR task started successfully' });
      } catch (error) {
            console.log(error);
            return res.json({ message: 'Error starting scrape CSR task' }).status(500);
      }
});

app.route('/ssr').get((req, res) => {
      try {

          const child_process = spawn(venvPythonPath, [path.join('ecommerce_scraper', 'tasks', 'ssrscrapetask.py')])

          child_process.stdout.on('data', (data) => {
          console.log(`stdout: ${data}`);
            });

              child_process.stderr.on('data', (data) => {
              console.error(`stderr: ${data}`);
            });

              child_process.on('close', (code) => {
              console.log(`child process exited with code ${code}`);
            });

            return res.json({ message: 'Scrape SSR task started successfully' });
      } catch (error) {
            console.log(error);
            return res.json({ message: 'Error starting scrape SSR task' }).status(500);
      }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
