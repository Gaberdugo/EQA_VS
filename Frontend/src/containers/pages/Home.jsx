import NavBar from "components/navigation/NavBar"
import Footer from "components/navigation/Footer"
import Layout from "hocs/Layouts/Layout"
import { connect } from "react-redux"

function Home(){
    return(
        <Layout>
            <NavBar/>
            <div className="pt-60 mb-60">
            </div>
            <Footer/>
        </Layout>
    )
}

const mapStateToProps=state=>({

})

export default connect(mapStateToProps, {
    
}) (Home)