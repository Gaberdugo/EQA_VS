import { connect  } from "react-redux";
import { Link } from "react-router-dom";
import logo from '../../assets/img/LogoFundacionTerpel.png'

function NavBar(){
    return(
        <nav className='w-full py-0 fixed'>
            <div className="px-8 sm:px-100" style={{background: '#F8F8F8'}} >
                <div className="-ml-4 -mt-2 flex flex-wrap items-center justify-between sm:flex-nowrap">
                    <div className="space-y-8 xl:col-span-1">
                        <img
                            className="h-20"
                            src={logo}
                            alt="Fundación Terpel"
                            style={{ width: '250px', height: 'auto' }} 
                        />
                    </div>

                    <div className="ml-4 mt-2 flex-shrink-0">
                        {/*
                    <button
                        type="button"
                        className="relative inline-flex items-center rounded-md border border-transparent bg-white text-gray-900 px-4 py-2 text-sm font-medium shadow-sm hover:bg-indigo-600 hover:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 mx-4"
                    >
                        SIVS
                    </button>*/}
                    <Link
                        to='/login'
                        type="button"
                        className="relative inline-flex items-center rounded-md border border-transparent bg-white text-gray-900 px-4 py-2 text-sm font-medium shadow-sm hover:bg-[#1B8830] hover:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    >
                        Ingresar
                    </Link>
                    </div>
                </div>
            </div>
        </nav>
    )
}

const mapStateToProps=state=>({

})

export default connect(mapStateToProps,{

}) (NavBar)