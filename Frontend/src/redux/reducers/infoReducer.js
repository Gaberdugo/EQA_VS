const initialState = {
  data: [],      // Para almacenar los proyectos obtenidos
  loading: false, // Estado de carga de los proyectos
  error: null,    // Para manejar errores de la API de proyectos

  // Estado para los reportes
  reportes: [],   // Para almacenar los reportes obtenidos
  loadingReportes: false, // Estado de carga de los reportes
  errorReportes: null,    // Para manejar errores de la API de reportes
};

const infoReducer = (state = initialState, action) => {
  switch (action.type) {
    // PROYECTOS
    case 'POST_PROYECTO_REQUEST': // Acción para cuando comienza la solicitud de proyecto
      return { ...state, loading: true };
    case 'POST_PROYECTO_SUCCESS': // Acción para cuando la solicitud de proyecto tiene éxito
      return { ...state, loading: false, data: [...state.data, action.payload] }; // Añadir el nuevo proyecto
    case 'POST_PROYECTO_FAILURE': // Acción para cuando la solicitud de proyecto falla
      return { ...state, loading: false, error: action.payload };

    // REPORTES
    case 'FETCH_REPORTE_LOADING': // Acción cuando empieza a cargar los reportes
      return { ...state, loadingReportes: true, errorReportes: null };
    case 'FETCH_REPORTE_SUCCESS': // Acción cuando la solicitud de reportes es exitosa
      return { ...state, loadingReportes: false, reportes: action.payload }; // Guardar los reportes
    case 'FETCH_REPORTE_FAILURE': // Acción cuando la solicitud de reportes falla
      return { ...state, loadingReportes: false, errorReportes: action.payload };
    
    default:
      return state;
  }
};

export default infoReducer;
