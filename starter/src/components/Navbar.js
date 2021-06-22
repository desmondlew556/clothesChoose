import React, {useState} from 'react';
import { Button } from './Button';
import { Link } from 'react-router-dom';
import './Navbar.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
function Navbar() {
    const [click, setClick] = useState(false);
    const [button, setButton] = useState(true);

    const closeMenu = () => setClick(false);
    const handleClick = () => setClick(!click);

    const showButton = () => {
        if (window.innerWidth <= 600) {
          setButton(false);
        } else {
          setButton(true);
        }
      };
    
    window.addEventListener('resize', showButton);

    return (
        <nav className='navbar'>
            <div className='navbar-container'>
                <Link to='/' className='navbar-logo' onClick = {closeMenu}>
                    <FontAwesomeIcon className="navbar-icons" icon="tshirt" />  ClothesChoose
                </Link>
                <div className='menu-icon' onClick = {handleClick}>
                    <FontAwesomeIcon className="navbar-icons" icon={click? 'times' : 'bars'} />
                </div>
                <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                    <li className='nav-item'>
                        <Link to='/' className='nav-links' onClick={closeMenu}>
                            Home
                        </Link>
                    </li>
                    <li className='nav-item'>
                        <Link to='/ranking' 
                        className='nav-links' 
                        onClick={closeMenu}>
                            Rankings
                        </Link>
                    </li>
                </ul>
            </div>
        </nav>
    )
}

export default Navbar;