import Footer from "components/navigation/Footer";
import Layout from "hocs/Layouts/Layout";
import '../../styles/error404.css';

function Error404() {
    return (
        <Layout>
            <div className="error-container">
                <h1 className="error-title">Error - 404</h1>
                <h2 className="error-subtitle">Página no encontrada</h2>
                <p className="error-message">Lo sentimos, la página que estás buscando no existe.</p>
            </div>
            <Footer />
        </Layout>
    );
}

export default Error404;
