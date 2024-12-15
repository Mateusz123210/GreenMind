import { PlantCard } from "@/components/PlantCard";
import { Stack, Typography } from "@mui/material";

export default function Page() {
    return (
        <Stack gap={3}>
            <Typography variant="h5">Rośliny</Typography>
            <Stack gap={2}>
                <PlantCard title="konopia włóknista" description="trzymać w wysokiej temperaturze"/>
                <PlantCard title="mak" description="przycinać łodygi co 3 tygodnie"/>
            </Stack>
        </Stack>
    );
}
