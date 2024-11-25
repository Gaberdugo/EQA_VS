import { combineReducers } from 'redux';
import auth from './auth';
import proyectosReducer from './proyectosReducer'; // Importar el nuevo reducer de proyectos
import infoReducer from './infoReducer';

export default combineReducers({
  auth,           // Mantener el reducer de auth
  proyectos: proyectosReducer, // Agregar el reducer de proyectos
  info: infoReducer,
});