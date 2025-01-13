import { logout } from "@/services/auth";
import { Button } from "@mui/material";

export const UserInfo: React.FC<{ email: string }> = ({ email }) => {
    return (
        <>
            {email}
            <Button onClick={logout} />
        </>
    );
};
