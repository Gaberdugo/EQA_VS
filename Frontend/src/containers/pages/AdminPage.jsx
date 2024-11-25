import Layout2 from "hocs/Layouts/Layout2"
import { connect } from "react-redux"

function Dashboard(){
    return(
        <Layout2/>
    )
}

const mapStateToProps=state=>({

})

export default connect(mapStateToProps,{

}) (Dashboard)