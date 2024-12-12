import "./Header.css"
import {Link} from "react-router-dom";

export const Header = () => {
    return (
        <nav className={"navbar"}>
            <div>
                <Link to={"/"}>
                    <img src="./logo-stockflow-main.png" alt="" width={80} height={80}/>
                    <img src="./logo-stockflow-secondary.png" alt="" height={43}/>
                </Link>


            </div>
        </nav>
    )
}