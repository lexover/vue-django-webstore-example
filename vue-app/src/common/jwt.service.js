const ID_TOKEN_KEY = 'jwt';

export const JwtService = {
  getToken: () => JSON.parse(window.localStorage.getItem(ID_TOKEN_KEY)),

  saveToken: (token) => window.localStorage.setItem(ID_TOKEN_KEY, JSON.stringify(token)),

  destroyToken: () => window.localStorage.removeItem(ID_TOKEN_KEY),

  parseJwt: (token) => {
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
      return null;
    }
  },

};

export default JwtService;
