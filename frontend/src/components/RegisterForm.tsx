import { isPasswordCorrect, register } from "@/services/auth";
import { Box, Button, TextField } from "@mui/material";
import { FormEvent, useState } from "react";

export const RegisterForm: React.FC<{ afterSubmit: () => void }> = ({ afterSubmit }) => {
    const onSubmit = (e: FormEvent<HTMLFormElement>) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const data = Object.fromEntries(new FormData(e.nativeEvent.target as any).entries());
        console.log(data);
        e.preventDefault();
        register(data.email as string, data.password as string);
        afterSubmit();
    };
    const [password, setPassword] = useState<string>("");
    return (
        <form onSubmit={onSubmit}>
            <Box p={1}>
                <TextField label="E-mail" type="email" name="email" />
            </Box>
            <Box p={1}>
                <TextField
                    label="hasło"
                    type="password"
                    name="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    error={!isPasswordCorrect(password)}
                    helperText={
                        isPasswordCorrect(password)
                            ? ""
                            : "Hasło musi zawierać małą literę, dużą literę, cyfrę, znak specjalny i mieć minimum 8 znaków"
                    }
                />
            </Box>
            <Button type="submit" fullWidth variant="contained">
                Zarejestruj
            </Button>
        </form>
    );
};
