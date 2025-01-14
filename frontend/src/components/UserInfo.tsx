import { logout } from "@/services/auth";
import { Box, Button, Stack } from "@mui/material";

export const UserInfo: React.FC<{ email: string }> = ({ email }) => {
    return (
        <Stack direction="row" gap={1}>
            {email}
            <Button onClick={logout} color="secondary" variant="contained">Wyloguj</Button>
        </Stack>
    );
};
