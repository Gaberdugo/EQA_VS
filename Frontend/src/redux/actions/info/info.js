import axios from 'axios';
// Acciones
export const POST_PROYECTO_REQUEST = 'POST_PROYECTO_REQUEST';
export const POST_PROYECTO_SUCCESS = 'POST_PROYECTO_SUCCESS';
export const POST_PROYECTO_FAILURE = 'POST_PROYECTO_FAILURE';

// Acción para hacer POST a la base de datos
export const postProyecto = (proyectoData) => async dispatch => {
  console.log('hola');
  // Inicia el estado de carga
  dispatch({ type: POST_PROYECTO_REQUEST });

  const config = {
      headers: {
          'Content-Type': 'application/json'
      }
  };

  const body = JSON.stringify(proyectoData);

  try {
      // Hacer la solicitud POST a la API
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/res/respuesta/`, body, config);

  } catch (err) {
      // Si ocurre un error, maneja el error
      console.error("Error al enviar los datos del proyecto:", err);
      throw err;  // Esto propaga el error al bloque catch en el handleSubmit.
  }
};

// Acción de éxito al obtener proyectos
const getProyectosSuccess = (proyectos) => ({
    type: 'FETCH_PROYECTOS_SUCCESS',
    payload: proyectos,
});

// Acción de error al obtener proyectos
const getProyectosFailure = (error) => ({
    type: 'FETCH_PROYECTOS_FAILURE',
    payload: error,
});

// Acción de carga (para mostrar un indicador de carga si es necesario)
const getProyectosLoading = () => ({
    type: 'FETCH_PROYECTOS_LOADING',
});

// Función que hace la solicitud a la API y despacha las acciones correspondientes
export const getProyectos = () => {
    return async (dispatch) => {
        dispatch(getProyectosLoading()); // Indicamos que estamos cargando datos

        try {
            // Hacemos la solicitud GET con Axios
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/auth/proyecto/`);

            // Transformamos los datos para que el campo nombreProyecto sea concatenado
            const proyectosTransformados = response.data.map(proyecto => ({
                id: proyecto.id,
                nombre: proyecto.nombre,  // Conservamos el nombre original del proyecto
                ciudades: proyecto.ciudades.map(ciudad => ({
                    nombreProyecto: `${ciudad.nombre}`,
                    departamento: `${ciudad.departamento.nombre}`  // Concatenamos ciudad + departamento
                }))
            }));

            // Guardamos los proyectos transformados en el estado
            localStorage.setItem('proyectos', JSON.stringify(proyectosTransformados));

            // Dispatch de los datos transformados
            dispatch(getProyectosSuccess(proyectosTransformados));

        } catch (error) {
            console.error("Error al obtener los proyectos: ", error);
            dispatch(getProyectosFailure(error.message));
        }
    };
};

// Acción cuando la solicitud de reportes está cargando
export const getReporteLoading = () => ({
    type: 'FETCH_REPORTE_LOADING',
  });
  
  // Acción cuando la solicitud de reportes es exitosa
  export const getReporteSuccess = (data) => ({
    type: 'FETCH_REPORTE_SUCCESS',
    payload: data,
  });
  
  // Acción cuando la solicitud de reportes falla
  export const getReporteFailure = (error) => ({
    type: 'FETCH_REPORTE_FAILURE',
    payload: error,
  });
  
  // Acción para obtener los reportes
  export const getReporte = () => {
    return async (dispatch) => {
      dispatch(getReporteLoading());  // Indicamos que estamos cargando los datos de los reportes
  
      try {
        // Realizamos la solicitud GET a la API para obtener los reportes
        const response = await axios.get("http://127.0.0.1:8000/res/respuesta/exportar/");
  
        // Si la respuesta es exitosa, despachamos los datos obtenidos
        dispatch(getReporteSuccess(response.data));
  
      } catch (error) {
        // Si ocurre un error, despachamos el error
        dispatch(getReporteFailure(error.message));
      }
    };
  };