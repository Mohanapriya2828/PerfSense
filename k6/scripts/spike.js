import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 10 },
    { duration: '5s', target: 200 },
    { duration: '20s', target: 200 },
    { duration: '10s', target: 10 },
  ],
};

export default function () {

  let users = http.get('http://127.0.0.1:8000/users');

  check(users, {
    'Users API - Status 200': (r) => r.status === 200,
  });

  let products = http.get('http://127.0.0.1:8000/products');

  check(products, {
    'Products API - Status 200': (r) => r.status === 200,
  });

  sleep(1);
}