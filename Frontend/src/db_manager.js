// const fetch = require('node-fetch'); // if you working on Node but not Browser

export class DBManager {
    constructor(host = "localhost", port = 3001) {
        this.uri = `http://${host}:${port}`;
        this.endpoints = {
            get_choice: `${this.uri}/get_choice`
        };
    }

    async get_choice(state) {
        
        const params = {
            state: state
        };

        const queryString = new URLSearchParams(params).toString();
        const res = await fetch(
            `${this.endpoints.get_choice}?${queryString}`
            // {mode: 'no-cors'}
        );
        const data = await res.json(); // TODO/
        return data;
    }
}