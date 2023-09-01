import { adminRoot } from "./config";
import { UserRole } from "../utils/auth.roles";

const data = [{
  id: "home",
  icon: "iconsminds-home",
  label: "HOME",
  to: `/home`,
},
{
  id: "statistics",
  icon: "iconsminds-statistic",
  label: "STATISTICS",
  to: `/statistics`,
},
{
  id: "horses",
  icon: "iconsminds-box-full",
  label: "HORSES",
  to: `/horses`,
},
{
  id: "reports",
  icon: "iconsminds-receipt-4",
  label: "REPORTS",
  to: `/reports`,
},
{
  id: "admin",
  icon: "iconsminds-gear",
  label: "ADMIN",
  to: `/admin`,
},


];
export default data;
