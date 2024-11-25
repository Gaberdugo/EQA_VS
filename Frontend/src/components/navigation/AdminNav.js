import { connect  } from "react-redux";
//import { Link } from "react-router-dom";

function AdminNav(){
    return(
        <nav className='w-full py-0 top-0 fixed'>
            <div className="bg-white px-4 sm:px-6">
                <div className="flex justify-center items-center">
                    Hola mundo
                </div>
            </div>
        </nav>
    )
}

const mapStateToProps=state=>({

})

export default connect(mapStateToProps,{

}) (AdminNav)