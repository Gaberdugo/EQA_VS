const initialState = {
  data: [],      // Para almacenar los proyectos obtenidos
  loading: false, // Estado de carga
  error: null,    // Para manejar errores de la API
};

// Reducer que maneja los proyectos
const proyectosReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'FETCH_PROYECTOS_LOADING':
      return { ...state, loading: true };
    case 'FETCH_PROYECTOS_SUCCESS':
      return { ...state, loading: false, data: action.payload };
    case 'FETCH_PROYECTOS_FAILURE':
      return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
};

export default proyectosReducer;
