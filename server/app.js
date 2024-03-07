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


app.route('/csr').post((req, res) => {
    const id = req.body.id;
    const website = req.body.website;
    try {
          const child_process = spawn(venvPythonPath, [path.join('ecommerce_scraper', 'tasks', 'csrscrapetask.py'), id, website], {
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
              if (code !== 0) {
                    fetch(`${process.env.SCRAPE_SENSE_API_URL}/scrape-tasks/crash/${id}`, {
                      method: 'PATCH',
                      headers: {
                        'Content-Type': 'application/json',
                        'x-api-key': process.env.SCRAPE_SENSE_API_KEY || '',
                      },
                    });
              }
            });

            return res.json({ message: 'Scrape CSR task started successfully' });
    } catch (error) {
            console.log(error);
            return res.status(500).json({ message: 'Error starting scrape CSR task' });
    }
});

app.route('/ssr').post((req, res) => {
    const id = req.body.id;
    const website = req.body.website;
    try {
          const child_process = spawn(venvPythonPath, [path.join('ecommerce_scraper', 'tasks', 'ssrscrapetask.py'), id, website], {
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
              if (code !== 0) {
                    fetch(`${process.env.SCRAPE_SENSE_API_URL}/scrape-tasks/crash/${id}`, {
                      method: 'PATCH',
                      headers: {
                        'Content-Type': 'application/json',
                        'x-api-key': process.env.SCRAPE_SENSE_API_KEY || '',
                      },
                    });
              }
            });

            return res.json({ message: 'Scrape SSR task started successfully' });
    } catch (error) {
            console.log(error);
            return res.status(500).json({ message: 'Error starting scrape SSR task' });
    }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
