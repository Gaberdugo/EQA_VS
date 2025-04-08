import {
  ChartBarIcon,
  HomeIcon,
  RssIcon,
  UsersIcon,
  TrashIcon,
  PencilIcon,
  ArrowUturnUpIcon,
  WalletIcon,
  ChartPieIcon,
} from '@heroicons/react/24/outline'
import { NavLink, useLocation } from 'react-router-dom'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

function Sidebar3(){

  const location = useLocation()

  const navigation = [
      { name: 'Validador', href: '/valPage', icon: HomeIcon, current: location.pathname==='/valPage' ? true:false },
      { name: 'Pruebas', href: '/pruebaPage', icon: RssIcon, current: location.pathname==='/pruebaPage' ? true:false },
      { name: 'Reporte G', href: '/reportPage', icon: WalletIcon, current: location.pathname==='/reportPage' ? true:false },
      { name: 'Reporte 1', href: '/reportPage1', icon: ChartBarIcon, current: location.pathname==='/reportPage1' ? true:false },
      { name: 'Reporte 2', href: '/reportPage2', icon: ChartPieIcon, current: location.pathname==='/reportPage2' ? true:false },
      { name: 'Digitadores', href: '/valDigi', icon: UsersIcon, current: location.pathname==='/valDigi' ? true:false },
      { name: 'Digitar', href: '/valForm', icon: PencilIcon, current: location.pathname==='/valForm' ? true:false },
      { name: 'Corregir', href: '/valCorr', icon: ArrowUturnUpIcon, current: location.pathname==='/valCorr' ? true:false },
      { name: 'Eliminar', href: '/valDelete', icon: TrashIcon, current: location.pathname==='/valDelete' ? true:false },
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
export default Sidebar3