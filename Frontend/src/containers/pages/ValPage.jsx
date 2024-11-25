import Layout4 from "hocs/Layouts/Layout4"
import { connect } from "react-redux"

function ValPage(){
    return(
        <Layout4/>
    )
}

const mapStateToProps=state=>({

})

export default connect(mapStateToProps,{

}) (ValPage)