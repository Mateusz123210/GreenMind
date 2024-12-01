import { ListItem, ListItemButton, ListItemText, SxProps, Theme } from "@mui/material";
import { grey } from "@mui/material/colors";
import React, { PropsWithChildren } from "react";
import { usePathname, useRouter } from 'next/navigation'


interface Props extends PropsWithChildren {
    href: string;
} 
const NavigationListItem: React.FC<Props> = ({ children, href }) => {
    
    const router = useRouter();
    const pathname = usePathname();
    const isActive = pathname.startsWith(href);
    const activeStyles: SxProps<Theme> = (t) => ({
        color: t.palette.secondary.dark,
        fontWeight: "bolder",
        bgcolor: grey["200"]
    });

    return (
        <ListItem disablePadding onClick={() => router.push(href)} sx={isActive ? activeStyles : {}}>
            <ListItemButton>
                <ListItemText disableTypography >
                    {children}
                </ListItemText>
            </ListItemButton>
        </ListItem>
    );
};

export default NavigationListItem;