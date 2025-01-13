"use client";
import { PlantCard } from "@/components/PlantCard";
import { Plant } from "@/types/rest";
import { LinearProgress, Stack, Typography } from "@mui/material";
import useSWR from "swr";

export default function Page() {
    const { data: plants, isLoading } = useSWR<Plant[]>("/api/plants");
    return (
        <Stack gap={3}>
            <Typography variant="h5">Rośliny</Typography>
            <Stack gap={2}>
                {isLoading && <LinearProgress />}
                <PlantCard
                    title="konopia włóknista"
                    description="trzymać w wysokiej temperaturze"
                />
                <PlantCard title="mak" description="przycinać łodygi co 3 tygodnie" />
                {plants?.map((plant) => (
                    <PlantCard key={plant.id} title={plant.name} description={plant.description} />
                ))}
            </Stack>
        </Stack>
    );
}
