import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '20s', target: 20 },
    { duration: '30s', target: 50 },
    { duration: '20s', target: 100 },
    { duration: '20s', target: 0 },
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