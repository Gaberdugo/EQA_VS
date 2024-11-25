import Layout3 from "hocs/Layouts/Layout3"
import { connect } from "react-redux"

function DigiPage(){
    return(
        <Layout3/>
    )
}

const mapStateToProps=state=>({

})

export default connect(mapStateToProps,{

}) (DigiPage)