import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

import Error404 from 'containers/errors/Error404';

import Home from 'containers/pages/Home';
import AdminPage from 'containers/pages/AdminPage';
import AdminDigi from 'containers/pages/AdminDigi';
import AdminPre from 'containers/pages/AdminPre';
import AdminCua from 'containers/pages/AdminCua';
import Login from 'containers/pages/Login';
import DigiPage from 'containers/pages/DigiPage';
import InfoLoad from 'containers/pages/InfoLoad';
import ValPage from 'containers/pages/ValPage';
import ReportPage from 'containers/pages/ReportPage';
import ReportPage1 from 'containers/pages/ReportPage1';
import ReportPage2 from 'containers/pages/ReportPage2';
import PruebaPage from 'containers/pages/PruebaPage';
import ValDigi from 'containers/pages/ValDigi';
import ValDelete from 'containers/pages/valDelete';
import ValForm from 'containers/pages/ValForm';
import ValCorr from 'containers/pages/ValCorr';
import ValInsti from 'containers/pages/valInsti';
import ValPassword from 'containers/pages/ValPassword';
import TerPage from 'containers/pages/TerPage';
import TerPrueba from 'containers/pages/TerPrueba';
import TerReport from 'containers/pages/TerReport';

import PrivateRoute from './components/PrivateRoute';
import { AnimatePresence } from 'framer-motion';


function AnimatedRoutes() {
    const location = useLocation();

    return (
        <AuthProvider>
            <AnimatePresence>
                <Routes location={location} key={location.pathname}>
                    {/* Cualquier otra ruta */}         
                    <Route path="*" element={<Error404 />} />
                    
                    {/* Ruta de inicio y de login */}
                    <Route path="/" element={<Home />} />
                    <Route path='/login' element={<Login />} />
                    
                    {/* Rutas prohibidas */} 
                    <Route
                        path="/admin"
                        element={
                            <PrivateRoute requiredRole="admin">
                                <AdminPage />
                            </PrivateRoute>
                        }
                    />

                    <Route
                        path='/adminDigi'
                        element={
                            <PrivateRoute requiredRole="admin">
                                <AdminDigi />
                            </PrivateRoute>
                        }
                    />

                    <Route
                        path='/adminPre'
                        element={
                            <PrivateRoute requiredRole="admin">
                                <AdminPre />
                            </PrivateRoute>
                        }
                    />

                    <Route
                        path='/adminCua'
                        element={
                            <PrivateRoute requiredRole="admin">
                                <AdminCua />
                            </PrivateRoute>
                        }
                    />

                    <Route
                        path="/digi"
                        element={
                            <PrivateRoute requiredRole="digitador">
                                <DigiPage />
                            </PrivateRoute>
                        }
                    />
                    <Route 
                        path='/infoLoad' 
                        element={
                            <PrivateRoute requiredRole="digitador">
                                <InfoLoad />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/valPage' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <ValPage />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/reportPage' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <ReportPage />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/reportPage1' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <ReportPage1 />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/reportPage2' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <ReportPage2 />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/pruebaPage' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <PruebaPage />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/valDigi' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <ValDigi />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/valForm' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <ValForm />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/valInsti' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <ValInsti />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/valCorr' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <ValCorr />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/valDelete' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <ValDelete />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/valPassword' 
                        element={
                            <PrivateRoute requiredRole="val">
                                <ValPassword />
                            </PrivateRoute>
                        } 
                    />

                    
                    <Route 
                        path='/terPage' 
                        element={
                            <PrivateRoute requiredRole="terpel">
                                <TerPage />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/terPrueba' 
                        element={
                            <PrivateRoute requiredRole="terpel">
                                <TerPrueba />
                            </PrivateRoute>
                        } 
                    />

                    <Route 
                        path='/terReport'
                        element={
                            <PrivateRoute requiredRole="terpel">
                                <TerReport />
                            </PrivateRoute>
                        } 
                    />                    

                </Routes>
            </AnimatePresence>
        </AuthProvider>
    );
}

export default AnimatedRoutes;