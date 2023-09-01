import api from '@/services/axios';

const AuthService = {
    login({ email, password }) {
        return api
            .post('/auth/login', {
                email,
                password,
            })
            .catch(err => {
                throw err;
            });
    },
    google() {
        return api.get('/auth/google').catch(err => {
            throw err;
        });
    },

    signUp({ username, email, password }) {
        return api
            .post('/auth/signup', {
                username,
                email,
                password,
            })
            .catch(err => {
                throw err;
            });
    },

    refreshToken() {
        return api.post('/auth/refresh-token').catch(err => {
            throw err;
        });
    },
};

export default AuthService;
