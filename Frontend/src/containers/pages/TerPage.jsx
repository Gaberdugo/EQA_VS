import Layout5 from "hocs/Layouts/Layout5"
import { connect } from "react-redux"

function ValPage(){
    return(
        <Layout5/>
    )
}

const mapStateToProps=state=>({

})

export default connect(mapStateToProps,{

}) (ValPage)