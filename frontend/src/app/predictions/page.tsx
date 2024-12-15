import { Paper, Stack, Typography } from "@mui/material";

export default function Page() {
    return (
        <Stack gap={3}>
            <Typography variant="h5" component="h2">
                Predykcje
            </Typography>
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6">Warunki zewnętrzne</Typography>
            </Paper>
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6">Warunki wewnętrzne</Typography>
            </Paper>
        </Stack>
    );
}
