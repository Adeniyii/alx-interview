#!/usr/bin/node
import { argv, exit } from 'process';
import r from 'request';

const baseURL = 'https://swapi-api.alx-tools.com/api/';
const filmID = argv[2];

async function doFetch (urls) {
  const reqQueue = [];

  for (const url of urls) {
    const f = new Promise((resolve, reject) => {
      r(url, {}, (err, _, bd) => {
        if (err) {
          reject(err.message);
        }
        resolve(JSON.parse(bd).name);
      });
    });
    reqQueue.push(f);
  }
  return Promise.allSettled(reqQueue);
}

function main () {
  r(baseURL + 'films/' + filmID, {}, (err, _, body) => {
    if (err) {
      console.log(err.message);
      exit(1);
    }
    const characters = JSON.parse(body).characters;
    doFetch(characters).then(v => {
      v.forEach(vv => vv.status === 'fulfilled' && console.log(vv.value));
    });
  });
}

main();
