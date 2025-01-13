import { logout } from "@/services/auth"
import { Button } from "@mui/material"

export const UserInfo = (email: string) => {
    return <>{email}<Button onClick={logout}/></>
}