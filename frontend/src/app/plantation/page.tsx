import { PlantationCard } from "@/components/PlantationCard";
import { Stack, Typography } from "@mui/material";

export default function Page() {
    return (
        <Stack gap={3}>
            <Typography variant="h5">Hodowle</Typography>
            <Stack gap={2}>
                <PlantationCard title="Hodowla 1"/>
                <PlantationCard title="Hodowla 2"/>
            </Stack>
        </Stack>
    );;
}
