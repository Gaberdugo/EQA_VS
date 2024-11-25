import { BrowserRouter as Router} from 'react-router-dom';
import store from './store';
import { Helmet, HelmetProvider} from 'react-helmet-async';
import { Provider } from 'react-redux'
import './styles/background.css'; 

import AnimatedRoutes from 'Routes'

function App() {
  return (
    <HelmetProvider>
      <Helmet>
        <title>EQA - Visión Social</title>
        <meta name="description" content="Programa de prueba visión social" />
      </Helmet>
      <Provider store={store}>
        <Router>
            <AnimatedRoutes/>
        </Router>
      </Provider>
    </HelmetProvider>
  );
}

export default App;
