#!/usr/bin/node
import { argv, exit } from 'process';
import r from 'request';

const baseURL = 'https://swapi-api.alx-tools.com/api/';
const filmID = argv[2];

r(baseURL + 'films/' + filmID, {}, (err, _, body) => {
  if (err) {
    console.log(err.message);
    exit(1);
  }
  const characters = JSON.parse(body).characters;
  for (const ch of characters) {
    r(ch, {}, (_, __, bd) => {
      console.log(JSON.parse(bd).name);
    });
  }
});
