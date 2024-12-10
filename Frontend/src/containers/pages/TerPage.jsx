import Layout5 from "hocs/Layouts/Layout5"
import { connect } from "react-redux"

function TerPage(){
    return(
        <Layout5/>
    )
}

const mapStateToProps=state=>({

})

export default connect(mapStateToProps,{

}) (TerPage)