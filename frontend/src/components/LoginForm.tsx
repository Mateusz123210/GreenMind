import { login } from "@/services/auth";
import { Box, Button, TextField } from "@mui/material";
import { FormEvent } from "react";

export const LoginForm: React.FC<{ afterSubmit: () => void }> = ({ afterSubmit }) => {
    const onSubmit = (e: FormEvent<HTMLFormElement>) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const data = Object.fromEntries(new FormData(e.nativeEvent.target as any).entries());
        console.log(data);
        e.preventDefault();
        login(data.email as string, data.password as string);
        afterSubmit();
    };
    return (
        <form onSubmit={onSubmit}>
            <Box p={1}>
                <TextField label="E-mail" type="email" name="email" />
            </Box>
            <Box p={1}>
                <TextField label="hasło" type="password" name="password" />
            </Box>
            <Button type="submit" fullWidth variant="contained">
                Zaloguj
            </Button>
        </form>
    );
};
