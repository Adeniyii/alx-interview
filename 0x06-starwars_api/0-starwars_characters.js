#!/usr/bin/node
const { argv } = require('process');
const r = require('request');

const baseURL = 'https://swapi-api.alx-tools.com/api/';
const filmID = argv[2];

/**
 * Fetches a list of urls and extracts a field from the response
 * @param {[string]} urls list of urls to fetch
 * @param {string} field field to extract from the response
 * @returns Promise with the list of values
 */
function doFetch (urls, field) {
  const reqQueue = [];

  for (const url of urls) {
    const f = new Promise((resolve, reject) => {
      r(url, {}, (err, _, bd) => {
        if (err) {
          reject(err.message);
        }
        resolve(JSON.parse(bd)[field]);
      });
    });
    reqQueue.push(f);
  }
  return Promise.allSettled(reqQueue);
}

function main () {
  doFetch([`${baseURL}films/${filmID}`], 'characters').then(v => {
    const characters = v[0].value;
    doFetch(characters, 'name').then(v => {
      v.forEach(vv => vv.status === 'fulfilled' && console.log(vv.value));
    });
  });
}

main();
