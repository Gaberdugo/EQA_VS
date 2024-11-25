import {
    HomeIcon,
    UsersIcon,
    QuestionMarkCircleIcon,
    BookOpenIcon
  } from '@heroicons/react/24/outline'
import { NavLink, useLocation } from 'react-router-dom'


function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
}

function Sidebar(){

    const location = useLocation()

    const navigation = [
        { name: 'Admin', href: '/admin', icon: HomeIcon, current: location.pathname==='/admin' ? true:false },
        { name: 'Usuarios', href: '/adminDigi', icon: UsersIcon, current: location.pathname==='/adminDigi' ? true:false },
        { name: 'Preguntas', href: '/adminPre', icon: QuestionMarkCircleIcon, current: location.pathname==='/adminPre' ? true:false },
        { name: 'Cuadernillos', href: '/adminCua', icon: BookOpenIcon, current: location.pathname==='/adminCua' ? true:false },
    ]

    return(
        <div>
            {navigation.map((item) => (
                  <NavLink
                    key={item.name}
                    to={item.href}
                    className={classNames(
                      item.current ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900',
                      'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
                    )}
                  >
                    <item.icon
                      className={classNames(
                        item.current ? 'text-gray-500' : 'text-gray-400 group-hover:text-gray-500',
                        'mr-3 flex-shrink-0 h-6 w-6'
                      )}
                      aria-hidden="true"
                    />
                    {item.name}
                  </NavLink>
            ))}
        </div>
    )
}
export default Sidebar